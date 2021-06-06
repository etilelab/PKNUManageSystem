--------------------------------------------------------------------------------------
-- Name	       : OT (Oracle Tutorial) Sample Database
-- Link	       : http://www.oracletutorial.com/oracle-sample-database/
-- Version     : 1.0
-- Last Updated: July-28-2017
-- Copyright   : Copyright ?2017 by www.oracletutorial.com. All Rights Reserved.
-- Notice      : Use this sample database for the educational purpose only.
--               Credit the site oracletutorial.com explitly in your materials that
--               use this sample database.
--------------------------------------------------------------------------------------

CREATE DATABASE pknu default CHARACTER SET UTF8;
use pknu;

CREATE TABLE board (
    write_id VARCHAR(50) NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content VARCHAR(2000) NOT NULL,
    employee_id INT NOT NULL,
    write_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    notice int default 0,
	FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);

CREATE TABLE best_customer (
    customer_id INT NOT NULL,
    best_date VARCHAR(255) NOT NULL,
    best_rank DOUBLE,
	FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    PRIMARY KEY(customer_id, best_date)
);

CREATE TABLE best_employee(
    employee_id INT NOT NULL,
    best_date VARCHAR(255) NOT NULL,
    best_rank DOUBLE,
	FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
    PRIMARY KEY(employee_id, best_date)
);

CREATE TABLE member (
    email VARCHAR(50) NOT NULL PRIMARY KEY,
    passwd VARCHAR(255) NOT NULL,
    employee_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);


CREATE TABLE regions
  (
    region_id INT PRIMARY KEY ,
    region_name VARCHAR( 50 ) NOT NULL
  );
-- countries table
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE countries
  (
    country_id   CHAR( 2 ) PRIMARY KEY  ,
    country_name VARCHAR( 40 ) NOT NULL,
    region_id  INT                 , -- fk
    CONSTRAINT fk_countries_regions FOREIGN KEY( region_id )
      REFERENCES regions( region_id )
      ON DELETE CASCADE
  );



CREATE TABLE locations
  (
    location_id INT  PRIMARY KEY       ,
    address     VARCHAR( 255 ) NOT NULL,
    postal_code VARCHAR( 20 )          ,
    city        VARCHAR( 50 )          ,
    state       VARCHAR( 50 )          ,
    country_id  CHAR( 2 )               , -- fk
    CONSTRAINT fk_locations_countries
      FOREIGN KEY( country_id )
      REFERENCES countries( country_id )
      ON DELETE CASCADE
  );
-- warehouses
-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE warehouses
  (
    warehouse_id INT PRIMARY KEY,
    warehouse_name VARCHAR( 255 ) ,
    location_id    INT, -- fk
    CONSTRAINT fk_warehouses_locations
      FOREIGN KEY( location_id )
      REFERENCES locations( location_id )
      ON DELETE CASCADE
  );
-- employees
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE employees
  (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR( 255 ) NOT NULL,
    last_name  VARCHAR( 255 ) NOT NULL,
    email      VARCHAR( 255 ) NOT NULL,
    phone      VARCHAR( 50 ) NOT NULL ,
    hire_date  DATETIME NOT NULL          ,
    manager_id INT        , -- fk
    job_title  VARCHAR( 255 ) NOT NULL,
    CONSTRAINT fk_employees_manager
        FOREIGN KEY( manager_id )
        REFERENCES employees( employee_id )
        ON DELETE CASCADE
  );
-- product category
-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE product_categories
  (
    category_id INT PRIMARY KEY,
    category_name VARCHAR( 255 ) NOT NULL
  );

-- products table
-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE products
  (
    product_id INT PRIMARY KEY,
    product_name  VARCHAR( 255 ) NOT NULL,
    description   VARCHAR( 2000 )        ,
    standard_cost DECIMAL( 9, 2 )          ,
    list_price    DECIMAL( 9, 2 )          ,
    category_id   INT NOT NULL         ,
    likes INT,
    views INT,
    discount_price DOUBLE,
    CONSTRAINT fk_products_categories
      FOREIGN KEY( category_id )
      REFERENCES product_categories( category_id )
      ON DELETE CASCADE
  );
-- customers
-- SQLINES LICENSE FOR EVALUATION USE ONLY


CREATE TABLE customers
  (
    customer_id INT PRIMARY KEY,
    name         VARCHAR( 255 ) NOT NULL,
    address      VARCHAR( 255 )         ,
    website      VARCHAR( 255 )         ,
    credit_limit DECIMAL( 8, 2 ),
    city VARCHAR(255)
  );

-- contacts
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE contacts
  (
    contact_id INT PRIMARY KEY,
    first_name  VARCHAR( 255 ) NOT NULL,
    last_name   VARCHAR( 255 ) NOT NULL,
    email       VARCHAR( 255 ) NOT NULL,
    phone       VARCHAR( 20 )          ,
    customer_id INT                  ,
    CONSTRAINT fk_contacts_customers
      FOREIGN KEY( customer_id )
      REFERENCES customers( customer_id )
      ON DELETE CASCADE
  );
-- orders table
-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE orders
  (
    order_id INT PRIMARY KEY,
    customer_id INT, -- fk
    status  VARCHAR( 20 ) NOT NULL ,
    salesman_id INT         , -- fk
    order_date  DATETIME NOT NULL          ,
    employee_order INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_orders_customers
      FOREIGN KEY( customer_id )
      REFERENCES customers( customer_id )
      ON DELETE CASCADE,
    CONSTRAINT fk_orders_employees
      FOREIGN KEY( salesman_id )
      REFERENCES employees( employee_id )
      ON DELETE SET NULL
  );

-- order items
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE order_items
  (
    order_id   INT                                , -- fk
    item_id    INT                                ,
    product_id INT NOT NULL                       , -- fk
    quantity   DECIMAL( 8, 2 ) NOT NULL                        ,
    unit_price DECIMAL( 8, 2 ) NOT NULL                        ,
    CONSTRAINT pk_order_items
      PRIMARY KEY( order_id, item_id ),
    CONSTRAINT fk_order_items_products
      FOREIGN KEY( product_id )
      REFERENCES products( product_id )
      ON DELETE CASCADE,
    CONSTRAINT fk_order_items_orders
      FOREIGN KEY( order_id )
      REFERENCES orders( order_id )
      ON DELETE CASCADE
  );
-- inventories
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE inventories
  (
    product_id   INT        , -- fk
    warehouse_id INT        , -- fk
    quantity     INT NOT NULL,
    CONSTRAINT pk_inventories
      PRIMARY KEY( product_id, warehouse_id ),
    CONSTRAINT fk_inventories_products
      FOREIGN KEY( product_id )
      REFERENCES products( product_id )
      ON DELETE CASCADE,
    CONSTRAINT fk_inventories_warehouses
      FOREIGN KEY( warehouse_id )
      REFERENCES warehouses( warehouse_id )
      ON DELETE CASCADE
  );


SET FOREIGN_KEY_CHECKS=0;
SET FOREIGN_KEY_CHECKS=1;
commit;
