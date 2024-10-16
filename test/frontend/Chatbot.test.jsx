// Chatbot.ui.test.jsx
import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Chatbot from './src/components/Chatbot';

describe('Chatbot Component UI Tests', () => {
  test('renders the chat button with the correct initial text', () => {
    render(<Chatbot />);
    
    // Verify the chat button is present with text "Chat"
    const chatButton = screen.getByText('Chat');
    expect(chatButton).toBeInTheDocument();
  });

  test('toggles chat window when button is clicked', () => {
    render(<Chatbot />);
    
    const chatButton = screen.getByText('Chat');

    // Click to open the chat window
    fireEvent.click(chatButton);
    expect(screen.getByPlaceholderText('Type a message...')).toBeInTheDocument();
    
    // Click again to close the chat window
    fireEvent.click(chatButton);
    expect(screen.queryByPlaceholderText('Type a message...')).not.toBeInTheDocument();
  });

  test('input field is empty by default and updates correctly', () => {
    render(<Chatbot />);
    
    // Open the chat window
    fireEvent.click(screen.getByText('Chat'));
    
    const inputField = screen.getByPlaceholderText('Type a message...');
    
    // Verify the input field is initially empty
    expect(inputField.value).toBe('');

    // Change the input value
    fireEvent.change(inputField, { target: { value: 'Hello' } });
    expect(inputField.value).toBe('Hello');
  });

  test('send button is present and clickable', () => {
    render(<Chatbot />);
    
    // Open the chat window
    fireEvent.click(screen.getByText('Chat'));
    
    // Check if the Send button is present
    const sendButton = screen.getByText('Send');
    expect(sendButton).toBeInTheDocument();
    
    // Click the send button (does not verify behavior, just checks interaction)
    fireEvent.click(sendButton);
  });

});
