DIR=$1 npm start

mkdir -p build/$1
cp -r $1/img build/$1/img
sed '3s/^/[View Report](Report.pdf)\n\n/' $1/README.md > build/$1/README.md
cp $1/README.pdf build/$1/Report.pdf