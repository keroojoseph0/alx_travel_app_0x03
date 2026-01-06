# alx_travel_app_0x01

##  Payment Workflow

1- User creates a Booking
	
2- System:

        Creates a Payment record (status = PENDING)
        
        Calls Chapa API to initialize payment
        
3- Chapa returns:

        transaction_id
        
        checkout_url
        
4- User:

        Opens checkout_url
        
        Pays on Chapa

5- Backend:

    Calls Chapa verify API
    
    Updates payment status:
    
    COMPLETED ✅
    
    or FAILED ❌
    
    On success:
    
    Send confirmation email (Celery background task)

👉 Rule:

Never trust the frontend. Always verify payment from backend.