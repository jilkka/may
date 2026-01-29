-- Add menu preference columns to users table
-- Run this if you get "no such column" errors

ALTER TABLE users ADD COLUMN start_page VARCHAR(50) DEFAULT 'dashboard';
ALTER TABLE users ADD COLUMN show_menu_vehicles BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN show_menu_fuel BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN show_menu_expenses BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN show_menu_reminders BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN show_menu_maintenance BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN show_menu_recurring BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN show_menu_documents BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN show_menu_stations BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN show_quick_entry BOOLEAN DEFAULT 0;
