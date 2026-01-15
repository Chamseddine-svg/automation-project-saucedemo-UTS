/**
 * @fileoverview Data loading utilities for test configuration
 * @description Loads and parses JSON test data and user configurations
 */

const fs = require('fs');
const path = require('path');

/**
 * Loads and parses a JSON file
 * @param {string} filename - Name of the JSON file to load
 * @returns {Object} Parsed JSON data
 * @throws {Error} If file cannot be read or parsed
 */
function loadJSON(filename) {
  try {
    const filePath = path.join(__dirname, '..', 'data', filename);
    const rawData = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(rawData);
  } catch (error) {
    throw new Error(`Failed to load ${filename}: ${error.message}`);
  }
}

/**
 * Loads test step data from steps.json
 * @returns {Object} Test steps configuration
 */
function loadSteps() {
  return loadJSON('steps.json');
}

/**
 * Loads user configuration from users.json
 * @returns {Object} User credentials and profiles
 */
function loadUsers() {
  return loadJSON('users.json');
}

/**
 * Gets a specific user by type
 * @param {string} userType - Type of user (standard, locked, problem, etc.)
 * @returns {Object} User credentials
 * @throws {Error} If user type is not found
 */
function getUserByType(userType) {
  const users = loadUsers();
  
  if (!users[userType]) {
    throw new Error(`User type '${userType}' not found in users.json`);
  }
  
  return users[userType];
}

/**
 * Gets application configuration
 * @returns {Object} Application config including base URL
 */
function getAppConfig() {
  const steps = loadSteps();
  return steps.config || {};
}

module.exports = {
  loadSteps,
  loadUsers,
  getUserByType,
  getAppConfig
};