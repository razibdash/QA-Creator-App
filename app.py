from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse 
import traceback
import uvicorn
import os
import aiofiles
import json
import csv
from src.helper import llm_pipeline


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# Create a root route to render the HTML file
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Create a route to handle the file upload and processing
@app.post("/upload")
async def chat(request: Request, pdf_file: bytes = File(), filename: str = Form(...)):
    base_folder = 'static/docs/'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    pdf_filename = os.path.join(base_folder, filename)

    async with aiofiles.open(pdf_filename, 'wb') as f:
        await f.write(pdf_file)
 
    response_data = jsonable_encoder(json.dumps({"msg": 'success',"pdf_filename": pdf_filename}))
    res = Response(response_data)
    return res


def get_csv(file_path):
    answer_generation_chain, ques_list = llm_pipeline(file_path)
    base_folder = 'static/output/'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    output_file = base_folder+"QA.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question", "Answer"])  # Writing the header row

        for question in ques_list:
            print("Question: ", question)
            answer = answer_generation_chain.run(question)
            print("Answer: ", answer)
            print("--------------------------------------------------\n\n")

            # Save answer to CSV file
            csv_writer.writerow([question, answer])
    return output_file

#generate the questions and answers from the pdf file
# @app.get("/generate")
# async def generate_questions(request: Request, pdf_filename: str = Form(...)):
#     if not pdf_filename:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PDF filename is required")
    
#     output_file = get_csv(pdf_filename)
#     response_data = jsonable_encoder(json.dumps({"output_file": output_file}))
#     res = Response(response_data)
#     return res

@app.post("/analyze")
async def analyze_pdf(pdf_filename: str = Form(...)):
    try:
        # Validate file exists
        if not os.path.exists(pdf_filename):
            raise HTTPException(status_code=400, detail=f"File not found: {pdf_filename}")
        
        # Run analysis
        output_file = get_csv(pdf_filename)

        # Return proper JSON response
        return JSONResponse(content={"output_file": output_file})
    
    except Exception as e:
        # Log error and return readable response
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")




if __name__ == "__main__":
  uvicorn.run("app:app", host="localhost", port=8000,reload=True,)