FROM python:3.9-slim

# Step 2: Install system dependencies for PyQt5 and threading libraries
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    apt-get install -y python3-tk x11-apps && \
    rm -rf /var/lib/apt/lists && \
    pip install --no-cache-dir -r requirements.txt
    
   

# Step 3: Set the working directory
WORKDIR /app

# Step 4: Copy requirements file into the container
COPY requirements.txt .

# Step 5: Install Python dependencies


# Step 6: Copy the rest of the application files into the container
COPY . .
# Expose the port that the app will run on
EXPOSE 5000

# Step 7: Define the command to run the app
CMD ["python", "main.py"]
