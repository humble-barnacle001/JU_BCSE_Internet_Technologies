./cmd.sh $1

mkdir -p build/$1
cp -r $1/img build/$1/img
cp $1/README.md build/$1/README.md
cp $1/README.pdf build/$1/Report.pdf