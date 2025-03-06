# Notes: Understanding Our Battery Covariate Data and Survival Model

## What’s in Our Data?

Our dataset (covariateData.mat) tracks battery performance using four key variables:  

* DischargeTime: Total hours a battery lasts until failure or degradation (e.g., 63–78 hours).  

* Temperature: Operating temperature (°C, e.g., 11–111°C), affecting wear rates.  

* Load: Electrical demand (likely kW, e.g., 1–32), showing usage intensity.  

* Manufacturer: Battery maker (A, B, C), reflecting design or quality differences.

Together, these covariates paint a picture of how long batteries endure under specific conditions. The short DischargeTime range suggests a lab test or early failure point (e.g., capacity drop to 80%), not full lifespan.


## What It Means

This data captures how environmental and operational factors—temperature, load, and manufacturer—drive battery reliability. For example, a battery at 111°C and 30.463 kW (Manufacturer B) lasted 77.499 hours, while one at 11°C and 32.053 kW (Manufacturer C) lasted 67.385 hours. Higher temperatures or loads might shorten life, and manufacturers could vary in durability. It’s a snapshot of performance under stress, useful for predicting real-world behavior.


Our Model: Cox Survival Prediction
We used Python’s lifelines.CoxPHFitter to build a survival model. It:  

* Takes DischargeTime as the lifetime to predict.  

* Uses Temperature, Load, and Manufacturer (encoded as A/B/C) to estimate how these factors shift the risk of failure over time.  

* Assumes all batteries failed at their recorded DischargeTime (no censoring).

* The model outputs a survival curve—probability of a battery lasting past a given time—and median life estimates, based on these covariates.


## How It Estimates Remaining Battery Life

For a real case (e.g., 30 hours used, 60°C, 25 kW, Manufacturer B), we:  
Predict the survival curve: Shows chances of lasting longer.  

Calculate median life: Total hours until 50% failure probability (e.g., 75 hours total), then subtract usage (75 - 30 = 45 hours remaining).
This mirrors the MATLAB example, giving us a practical way to estimate remaining useful life (RUL) based on current conditions.


## Why It Matters
This model lets us forecast battery longevity and plan maintenance. By understanding how temperature, load, and manufacturer affect life, we can optimize usage or spot risky conditions (e.g., high heat). It’s a step toward data-driven decisions for battery management in real applications.

