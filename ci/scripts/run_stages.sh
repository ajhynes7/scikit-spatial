python_version="$1"

for stage in "lint_code" "lint_docs" "types" "readme" "doctests" "unit" "property" "docs"
    bash $(pwd)/ci/scripts/run_stage.sh $stage $TRAVIS_PYTHON_VERSION
done