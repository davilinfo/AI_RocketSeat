# Use AWS base image for Python 3.12
FROM public.ecr.aws/lambda/python:3.12

#Install build-essential compiler and tools
RUN microdnf update -y && microdnf install -y gcc-c++ make

#Copy requirements.txt

COPY requirements.txt ${LAMBDA_TASK_ROOT}

#Install packages
RUN pip install -r requirements.txt

#Copy 
COPY travelAgent.py ${LAMBDA_TASK_ROOT}

#set permissions to make file executable
RUN chmod +x travelAgent.py

#Set the CMD to your handler
CMD [ "travelAgent.lambda_handler" ]