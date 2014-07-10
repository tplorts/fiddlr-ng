echo ">>) Compiling LESS into CSS"
cd home/static/my/styles
lessc -x styles.less styles.compiled.css
echo ">>) collectstatic"
cd ../../../../
python manage.py collectstatic
echo ">>) S3 synchronization"
aws s3 sync staticfiles/ s3://fiddlr --acl public-read
