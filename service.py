import logging
import threading
import sys
from datetime import datetime
import os
import schedule
import time

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
import requests

from modem import automateModem, restartModem, turnOffCharger, turnOnCharger, isModemReachable

# Configure logging
# Clear any existing handlers to ensure fresh configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create log filename with current date
current_date = datetime.now().strftime('%Y-%m-%d')
log_filename = f'logs/service_{current_date}.log'

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Create file handler with append mode
file_handler = logging.FileHandler(log_filename, mode='a')
file_handler.setFormatter(formatter)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Configure root logger
logging.root.setLevel(logging.INFO)
logging.root.addHandler(file_handler)
logging.root.addHandler(console_handler)

app = FastAPI(
    title="ModemPower API",
    description="Smart modem power management system with battery monitoring and automated charging",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    """Initialize scheduler when the application starts"""
    setup_scheduler()

# Pydantic models for API documentation
class StatusResponse(BaseModel):
    status: str
    message: str

class BatteryResponse(BaseModel):
    status: str
    battery: int = None
    message: str

class ChargerResponse(BaseModel):
    status: str
    message: str
    internet_connected: bool = None

def send_email_notification(subject, message):
    """Send email notification via Brevo API"""
    try:
        brevo_api_key = os.getenv('BREVO_API_KEY')
        sender_email = os.getenv('SENDER_EMAIL')
        sender_name = os.getenv('SENDER_NAME', 'ModemPower')
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        recipient_name = os.getenv('RECIPIENT_NAME', 'User')
        
        if not all([brevo_api_key, sender_email, recipient_email]):
            logging.warning("Brevo configuration missing, skipping notification")
            return False
        
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            'accept': 'application/json',
            'api-key': brevo_api_key,
            'content-type': 'application/json'
        }
        
        data = {
            "sender": {
                "name": sender_name,
                "email": sender_email
            },
            "to": [
                {
                    "email": recipient_email,
                    "name": recipient_name
                }
            ],
            "subject": subject,
            "htmlContent": f"""
            <html>
            <head></head>
            <body>
                <h2>🚨 ModemPower Alert</h2>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Message:</strong> {message}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>
                <hr>
                <p><em>This is an automated message from ModemPower system.</em></p>
            </body>
            </html>
            """
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 201:
            logging.info(f"Brevo email notification sent successfully: {subject}")
            return True
        else:
            logging.error(f"Brevo API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logging.error(f"Failed to send Brevo email notification: {e}")
        return False


@app.get("/automate-modem", response_model=BatteryResponse, summary="Run modem automation", description="Check battery level and automatically turn modem on/off based on battery percentage")
def automate_modem():
    """Run modem automation - checks battery and turns on/off accordingly"""
    result = automateModem()
    return BatteryResponse(**result)


@app.get("/restart-modem", response_model=StatusResponse, summary="Restart modem", description="Restart the modem device")
def restart_modem():
    """Restart the modem device"""
    success = restartModem()
    if success:
        return StatusResponse(status="success", message="Modem restart initiated")
    else:
        return StatusResponse(status="error", message="Failed to restart modem")


@app.get("/scheduler-status", response_model=StatusResponse, summary="Scheduler status", description="Check if the scheduler is running and show next scheduled jobs")
def scheduler_status():
    """Check scheduler status and show next scheduled jobs"""
    try:
        jobs = schedule.get_jobs()
        if jobs:
            job_info = []
            for job in jobs:
                job_info.append(f"{job.job_func.__name__} - {job.next_run}")
            return StatusResponse(
                status="success", 
                message=f"Scheduler is running. Active jobs: {'; '.join(job_info)}"
            )
        else:
            return StatusResponse(
                status="warning", 
                message="Scheduler is running but no jobs are scheduled"
            )
    except Exception as e:
        return StatusResponse(
            status="error", 
            message=f"Scheduler error: {str(e)}"
        )


@app.get("/turn-off-charger", response_model=ChargerResponse, summary="Turn off charger", description="Turn off the smart charger/plug")
def turn_off_charger():
    """Turn off the smart charger/plug"""
    result = turnOffCharger()
    return ChargerResponse(**result)

@app.get("/turn-on-charger", response_model=ChargerResponse, summary="Turn on charger", description="Turn on the smart charger/plug with modem reachability check")
def turn_on_charger():
    """Turn on the smart charger/plug with modem reachability check"""
    # Check if modem is reachable before turning on
    if not isModemReachable():
        logging.error("Modem is not reachable, sending notification")
        send_email_notification(
            "Modem Unreachable - Manual Intervention Required",
            "The modem at 192.168.1.1 is not reachable. Please manually turn on the modem."
        )
        return ChargerResponse(
            status="error",
            message="Modem not reachable, email notification sent",
            internet_connected=False
        )

    result = turnOnCharger()
    return ChargerResponse(**result)


@app.get("/", summary="Home", description="Redirects to Swagger UI documentation")
def main():
    """Redirect to Swagger UI documentation"""
    return RedirectResponse(url="/docs")


def run_scheduler():
    """Run the scheduler in a separate thread"""
    logging.info("Scheduler thread started")
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
            time.sleep(30)


def setup_scheduler():
    """Setup scheduled tasks"""
    # Schedule turn-on-charger every 4 hours
    schedule.every(4).hours.do(turn_on_charger)
    
    # Schedule automate-modem every 5 minutes
    schedule.every(5).minutes.do(automateModem)
    
    logging.info("Scheduler setup complete:")
    logging.info("- Every 4 hours turn-on-charger")
    logging.info("- Automate-modem every 5 minutes")
    
    # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    logging.info(f"Scheduler thread started: {scheduler_thread.is_alive()}")


if __name__ == '__main__':
    import uvicorn
    
    # Start the FastAPI service with uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8765, log_level="info")
