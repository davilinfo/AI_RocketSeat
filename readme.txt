#create docker image as bellow
docker build --platform linux/x86_64 -t travelagent .

#ecr Amazon elastic container registry
#create a repository travelagent
#utilize aws-cli   (command line interface)  

#install aws-cli
#create IAM user, create access key
#run aws configure
#inform access key id and secret
#aws region name (us-east-1)
#enter
#add policies to user AmazonElasticContainerRegistryPublicFullAccess AmazonEC2ContainerRegistryFullAccess 

#access aws console ecr
#private repository and view push commands
#create environment variable OPENAI_API_KEY
#execute push commands as specified there until push the image into aws repository

#access lambda functions
#create a function based in container image
#edit function configuration increase time and memory

#for internet exposure create an alb in aws and adjust lambda_handler method accordingly then update image in aws and lambda