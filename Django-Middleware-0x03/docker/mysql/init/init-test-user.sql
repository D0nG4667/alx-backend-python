-- Create dedicated test user
CREATE USER IF NOT EXISTS 'testuser'@'%' IDENTIFIED BY 'strongpassword';

-- Create the test database
CREATE DATABASE IF NOT EXISTS test_alxmessaging
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Grant privileges only on the test DB
GRANT ALL PRIVILEGES ON test_alxmessaging.* TO 'testuser'@'%';

-- Allow CREATE/DROP for test DB lifecycle
GRANT CREATE, DROP ON *.* TO 'testuser'@'%';

-- Apply changes
FLUSH PRIVILEGES;
