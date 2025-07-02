#!/bin/bash

git clone https://github.com/Trinadtsaty/WhatWhereWhen.git
mkdir -p ~/temp_www
mv ~/WhatWhereWhen/* ~/temp_www/
rm -rf ~/WhatWhereWhen
cd ~/temp_www
mv WhatWhereWhen ..
cd ..
rm -rf ~/temp_www
cd ~/WhatWhereWhen
