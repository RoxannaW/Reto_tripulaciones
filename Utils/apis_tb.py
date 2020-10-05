import pandas as pd
import os, sys
from flask import Flask, render_template, redirect, request, jsonify 
import time
import random
import json

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)

def data_to_json(Data):
    Data.to_json(str(Data)+".json")

def dfjson(df):
    mean_per_day = df.groupby("date")["total_cases"].mean() #calculating mean per day of all countries
    mean_per_day.to_json("C:\\Users\\Roxan\\OneDrive\\Documentos\\Repo_August_project\\Project_August_Corona\\Roxanna\\Resources\\mean.json") #converting to Json mean
    return "se ha cargado el archivo mean.json en el path"