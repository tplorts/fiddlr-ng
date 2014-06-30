echo " == Compiling LESS into CSS"
cd home/static/my/styles
lessc -x styles.less styles.compiled.css


echo " == my static files"
cd ../..
aws s3 sync . s3://fiddlr-static   --exclude "node_modules/*"    --acl public-read

echo " == admin static files"
cd ../..
aws s3 sync venv/lib/python2.7/site-packages/django/contrib/admin/static/ s3://fiddlr-static --acl public-read
