# Crear bucket de S3 para cargar documentos
aws s3 mb s3://your-bucket-name --profile your-profile

# Validar Bucket Creado
aws s3 ls --profile your-profile

# Cargar Documento
aws s3 cp your-file.ext s3://<your-bucket-name>/path/ --profile your-profile

# Cargar Varios documentos a la vez
aws s3 cp your-path-file s3://<your-bucket-name>/path/ --recursive --profile your-profile

# Validar Carga de documentos
aws s3 ls s3://<your-bucket-name>/path/ --profile your-profile
