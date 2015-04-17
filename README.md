# ISI Store
This repostory contain the source code part of project in course *COMP321 Information System Implementation*.

> This project aims at providing an elegant online shopping experience to tentative customers. 
> The system contains one vendor and multiple potential customers. And the interaction 
> between the two parties can be stated as follows. The vendor displays the products in a 
> manner which is easy for customers to select product items, place orders, and make 
> purchases. The major products available in our website are routers, including wired and 
> wireless. They could be classified by brand names, wireless speed (for wireless routers), 
> WAN/LAN speed, CPU models, etc. Customers could select any routers they prefer and 
> place their orders.

## Demo
A online demo is avaiable at [isi.sorz.org](https://isi.sorz.org/).

## Install

0. Download repository
  ```
  git clone https://github.com/sorz/isi.git
  ```

1. Install [Python](https://www.python.org/) 3.4 or above
  ```
  apt-get install python3 python3-virtualenv
  ```

2. (Optional) Create virtual environments
   ```
   virtualenv env
   . env/bin/activate
   ```

2. Install Python modules
  ```
  pip install -r requirements.txt
  ```

3. Copy a config file and edit it
  ```
  cd store/store/settings
  cp config.sample.py config.py
  vim config.py
  ```

4. Install JavaScript librarys
  ```
  python manage.py bower install
  ```

5. Migrate database
  ```
  python manage.py migrate
  ```

6. (Optional) Load demo data
  ```
  python manage.py loaddata /path/to/data.json
  ```

7. Run
  ```
  python manage.py runserver
  ```

