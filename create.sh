#!/bin/bash
PROJECT_NAME=$1
mkdir -p $PROJECT_NAME/
cp template/template.h $PROJECT_NAME/$1.h
cp template/template.c $PROJECT_NAME/$1.c
cp template/template.py $PROJECT_NAME/$1.py
cp template/cy_template.pyx $PROJECT_NAME/cy_$1.pyx
cp config/template.ini config/$PROJECT_NAME.ini

sed -i "s/package *= *template/package = $PROJECT_NAME/" config/$PROJECT_NAME.ini
sed -i "s/env_name *= *template/env_name = $PROJECT_NAME/" config/$PROJECT_NAME.ini

PROJECT_NAME_CAMEL="$(tr '[:lower:]' '[:upper:]' <<< ${PROJECT_NAME:0:1})${PROJECT_NAME:1}"

for file in $PROJECT_NAME/$1.h $PROJECT_NAME/$1.c $PROJECT_NAME/$1.py $PROJECT_NAME/cy_$1.pyx; do
    sed -i "s/Template/$PROJECT_NAME_CAMEL/g" $file    
    sed -i "s/template/$PROJECT_NAME/g" $file    
    if [[ $file == *"cy_$1.pyx" ]]; then
        sed -i "s/cdef extern from \"$PROJECT_NAME.h\"/cdef extern from \"$1.h\"/g" $file
    fi
done

NEW_EXTENSION_PATH="'$PROJECT_NAME/cy_$1',"
sed -i "/^ *extension_paths *= *\[/a\\\ \\ \\ \\ $NEW_EXTENSION_PATH" setup.py

echo "from $PROJECT_NAME.$PROJECT_NAME import $PROJECT_NAME_CAMEL" >> policies/environment.py.tmp
cat policies/environment.py >> policies/environment.py.tmp
mv policies/environment.py.tmp policies/environment.py

sed -i "s/MAKE_FNS = {/MAKE_FNS = {\n    '$PROJECT_NAME': $PROJECT_NAME_CAMEL,/" policies/environment.py

echo "Project $PROJECT_NAME created"
echo "Don't forget:"
echo "    Actually add code to the $PROJECT_NAME.h file to fully describe the environment"
echo "    Add any observations (what the agent can 'see') to the compute_observations function"
echo "    Add any rendering logic to the c_render function"
echo "    Add any logging info to the Log struct in both the cy_$PROJECT_NAME.pyx and $PROJECT_NAME.h files"
echo "    Next, run 'python setup.py build_ext --inplace' to compile the new environment"
echo "    Then, run 'python demo.py --mode train --env $PROJECT_NAME' to train a policy on the new environment"
