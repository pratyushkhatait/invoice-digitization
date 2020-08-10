# SMS-Service #
Implementation of an invoice digitization service in Django.
## Dependencies ##
    -Python3
    -Django

## Steps ##
1. Create and activate a Virtual environment:
    - sudo apt-get install virtualenv
    - virtualenv -p python3 venv
    - source venv/bin/activate
2. Clone git repo
    - git clone  https://github.com/pratyushkhatait/invoice-digitization.git
3. Install requirements.txt
    - pip install -r requirements.txt
4. Django runserver
    - python manage.py runserver
5. Create any sample invoice pdf file
6. Call APIs hosted at: http://127.0.0.1:8000/
    1. Collect invoice(pdf document) from end customer using below POST API:
        http://127.0.0.1:8000/invoice-digitization/collect-invoice/
    2. Check status(i.e. Digitized or not) of given invoice document using below GET API:
        http://127.0.0.1:8000/invoice-digitization/invoice-status/?invoice_number=85677d60-06af-4cbb-8c26-e704057031b7
    3. Update invoice data using below POST API:
        http://127.0.0.1:8000/invoice-digitization/update-invoice/
    4. Fetch invoice details using below GET API:
        http://127.0.0.1:8000/invoice-digitization/invoice-details/?invoice_number=85677d60-06af-4cbb-8c26-e704057031b7
        
### Note: Attaching Postman collection for all the above APIS ###

