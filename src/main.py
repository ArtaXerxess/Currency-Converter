from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.ExchangeRateAPI import API

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

import json

with open("metadata/CurrencyNames.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)
    curr_dict = metadata.items()
    f.close()


# First/Home page
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    try:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "noError": True,
                "request": request,
                "curr_dict": curr_dict,
            },
        )
    except Exception as e:
        print(e)
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"noError": False, "Error": e},
        )


@app.post("/", response_class=HTMLResponse)
async def selectCurrency(
    request: Request, baseNumber: float = Form(...), baseCurrency: str = Form(...)
):
    try:
        print(f"base currency selected is {baseCurrency} and unit integer selected is {baseNumber}")
        
        # API Request
        api_instance = API(base=baseCurrency)
        print(json.dumps(obj=api_instance.getRates(),indent=4))


        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "noError": True,
                "curr_dict": curr_dict,
                "baseCurrencyResponse": f"Conversion for {baseNumber} {metadata[baseCurrency]['symbol_native']} {metadata[baseCurrency]['name']} 👇",
                "APIResponse":api_instance.getUpdateTimeStats(),
                "baseNumber":baseNumber,
                "ConversionTable":api_instance.getTable(),

            },
        )
    except Exception as e:
        print(e)
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "noError": False,
                "Error": e,
            },
        )
