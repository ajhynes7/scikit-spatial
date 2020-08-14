stages=(
    lint_code
    lint_docs
    types
    doctests
    unit_tests
    property_tests
)

for stage in ${stages[*]}; do

    docker build -t $stage --target $stage .
    docker run $stage

    if [ $? -ne 0 ]; then
        exit 1
    fi

done
