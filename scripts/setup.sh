force=false

while getopts "f" opt; do
  case $opt in
    f) force=true
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ ! -d excerpts ] || [ $force == true ]; then
    python excerpter.py
fi
