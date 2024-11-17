import csv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime

from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()
data_file = "senzori.txt"

class SensorData(BaseModel):
    timestamp: datetime 
    sensor_type: str
    value: float


# sensor_data_store: List[SensorData] = []

def write_data_to_file(data: SensorData):
    with open(data_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([data.timestamp.isoformat(), data.sensor_type, data.value])

def read_data_from_file() -> List[SensorData]:
    data = []
    try:
        with open(data_file, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 3:
                  continue
                timestamp, sensor_type, value = row
                try:
                    data.append(SensorData(
                        timestamp=datetime.fromisoformat(timestamp),
                        sensor_type=sensor_type, 
                        value=float(value)))
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return data[-5:]

@app.post("/data")
async def post_sensor_data(data: SensorData):
    
    write_data_to_file(data)
    return {data}

@app.get("/data/last5", response_model=List[SensorData])
async def get_last_5_sensors_data():
    try:
        data = read_data_from_file()
        if not data:
            raise HTTPException(status_code=404, detail="No data")
        #return data

        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title> Sensor Data </title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #d4ac7b; 
                    color: #333;
                }
                table {
                    widith: 100%;
                    border-collapse: collapse; 
                    margin-top: 20px;
                }
                th, td {
                    border: 1px solid #ddd; 
                    padding: 8px; 
                    text-allign: center; 
                }
                th { 
                    background-color: #4CAF50;
                    color: white; 
                }
                tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
                tr:hover {
                    background-color: #ddd;
                }
            </style>
        </head>
        <body>
            <h1> Last 5 Sensors Data</h1>
            <table>
                <thead>
                    <tr>
                        <th> Timestamp </th>
                        <th> Sensor Type </th>
                        <th> Value </th>
                    </tr>
                </thead>
                <tbody>
        """

        for entry in data: 
            html_content += f"""
            <tr>
                <td>{entry.timestamp}</td>
                <td>{entry.sensor_type}</td>
                <td>{entry.value}</td>
            </tr>
            """
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """
        return HTMLResponse(content = html_content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data file not found")


