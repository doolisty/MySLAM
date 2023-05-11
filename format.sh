find ./include -iname *.h -o -iname *.cc | xargs clang-format -style=google -i
find ./src -iname *.h -o -iname *.cc | xargs clang-format -style=google -i
