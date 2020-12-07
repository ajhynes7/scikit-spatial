python_version="$1"

for stage in "lint_code" "lint_docs" "types" "readme" "doctests" "unit" "property" "docs"; do
    bash $(pwd)/ci/scripts/run_stage.sh $stage $python_version || exit
done