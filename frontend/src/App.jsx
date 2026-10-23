import React, { useState } from 'react';

export default function App() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [createdUser, setCreatedUser] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    // Client-side validations
    const trimmedUsername = username.trim();
    const trimmedEmail = email.trim();

    if (!trimmedUsername || !trimmedEmail || !password) {
      setErrorMessage('All fields are required.');
      return;
    }

    if (trimmedUsername.length < 3 || trimmedUsername.length > 50) {
      setErrorMessage('Username must be between 3 and 50 characters.');
      return;
    }

    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(trimmedEmail)) {
      setErrorMessage('Please enter a valid email address.');
      return;
    }

    if (password.length < 8) {
      setErrorMessage('Password must be at least 8 characters long.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: trimmedUsername,
          email: trimmedEmail,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setErrorMessage(data.error || 'Registration failed. Please try again.');
      } else {
        setSuccessMessage('Account created successfully! You can now log in.');
        setCreatedUser(data.user);
        setUsername('');
        setEmail('');
        setPassword('');
      }
    } catch (err) {
      setErrorMessage('Network error: unable to connect to the server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="brand-header">
        <h1>SalonSync</h1>
        <p>Stylist Formula Notetaking & Sharing</p>
      </div>

      <h2 style={{ fontSize: '18px', marginBottom: '16px', textAlign: 'center' }}>
        Create Stylist Account
      </h2>

      {errorMessage && (
        <div className="banner banner-error" role="alert">
          {errorMessage}
        </div>
      )}

      {successMessage && (
        <div className="banner banner-success" role="status">
          <strong>{successMessage}</strong>
          {createdUser && (
            <div style={{ marginTop: '6px', fontSize: '12.5px' }}>
              Welcome, <strong>{createdUser.username}</strong> ({createdUser.email})!
            </div>
          )}
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="e.g. jsmith_color"
            required
            disabled={loading}
          />
          <div className="hint-text">3 to 50 characters, letters, numbers, and underscores.</div>
        </div>

        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="e.g. jsmith@example.com"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Minimum 8 characters"
            required
            disabled={loading}
          />
          <div className="hint-text">Must be at least 8 characters long.</div>
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>
    </div>
  );
}
