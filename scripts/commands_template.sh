# Crear bucket de S3 para plantilla de SAM IF NOT EXISTS
aws s3 mb s3://your-bucket-name --profile your-profile

# Validar Bucket Creado
aws s3 ls --profile your-profile

# Crear Layer para usar
aws lambda publish-layer-version --layer-name your-layer-name --zip-file fileb://layers/your-layer-file.zip --profile your-profile

# Validar Layer Creada
aws lambda list-layers --profile your-profile # Todas las creadas
aws lambda list-layer-versions --layer-name your-layer-name --profile your-profile # Una en específico

# Empaquetar Template
aws cloudformation package --s3-bucket your-bucket-name  --template-file poc_template.yaml --output-template-file gen2/template-generated.yaml --profile your-profile

# Desplegar Template
aws cloudformation deploy --template-file gen2/template-generated.yaml --stack-name your-stack-name --capabilities CAPABILITY_IAM --profile your-profile
