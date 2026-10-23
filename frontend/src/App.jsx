import React, { useState, useEffect } from 'react';

export default function App() {
  const [activeTab, setActiveTab] = useState('login'); // 'login' | 'signup'

  // Form fields
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Auth state
  const [token, setToken] = useState(() => localStorage.getItem('salonsync_token') || '');
  const [currentUser, setCurrentUser] = useState(null);

  // Status feedback
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Fetch current user if token exists on mount
  useEffect(() => {
    if (token) {
      fetchUser(token);
    }
  }, [token]);

  const fetchUser = async (authToken) => {
    try {
      const res = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });
      if (res.ok) {
        const data = await res.json();
        setCurrentUser(data.user);
      } else {
        handleLogout();
      }
    } catch (err) {
      handleLogout();
    }
  };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

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
        setSuccessMessage('Account created successfully! Logging you in...');
        if (data.token) {
          localStorage.setItem('salonsync_token', data.token);
          setToken(data.token);
          setCurrentUser(data.user);
        }
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

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    const identifier = (email || username).trim();

    if (!identifier || !password) {
      setErrorMessage('Email/Username and password are required.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: identifier,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setErrorMessage(data.error || 'Login failed. Please check your credentials.');
      } else {
        setSuccessMessage('Login successful!');
        localStorage.setItem('salonsync_token', data.token);
        setToken(data.token);
        setCurrentUser(data.user);
        setEmail('');
        setUsername('');
        setPassword('');
      }
    } catch (err) {
      setErrorMessage('Network error: unable to connect to the server.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout', { method: 'POST' });
    } catch (err) {
      // Ignore network errors on logout
    } finally {
      localStorage.removeItem('salonsync_token');
      setToken('');
      setCurrentUser(null);
      setSuccessMessage('Logged out successfully.');
      setErrorMessage('');
    }
  };

  return (
    <div className="container">
      <div className="brand-header">
        <h1>SalonSync</h1>
        <p>Stylist Formula Notetaking and Sharing</p>
      </div>

      {currentUser ? (
        <div style={{ textAlign: 'center' }}>
          <div className="banner banner-success">
            <strong>Active Session</strong>
            <div style={{ marginTop: '4px', fontSize: '13px' }}>
              Logged in as <strong>{currentUser.username}</strong> ({currentUser.email})
            </div>
            <div style={{ marginTop: '2px', fontSize: '12px', color: '#4a5568' }}>
              Role: <span>{currentUser.role}</span>
            </div>
          </div>

          <div style={{ padding: '20px 0', color: '#718096', fontSize: '14px' }}>
            Ready to record and organize your client color formulas.
          </div>

          <button
            type="button"
            className="btn-primary"
            onClick={handleLogout}
            style={{ backgroundColor: '#e53e3e' }}
          >
            Log Out
          </button>
        </div>
      ) : (
        <>
          <div style={{ display: 'flex', borderBottom: '1px solid #e2e8f0', marginBottom: '20px' }}>
            <button
              type="button"
              onClick={() => { setActiveTab('login'); setErrorMessage(''); setSuccessMessage(''); }}
              style={{
                flex: 1,
                padding: '10px',
                border: 'none',
                background: 'none',
                fontWeight: activeTab === 'login' ? '700' : '500',
                color: activeTab === 'login' ? '#2b6cb0' : '#718096',
                borderBottom: activeTab === 'login' ? '2px solid #2b6cb0' : 'none',
                cursor: 'pointer',
              }}
            >
              Stylist Login
            </button>
            <button
              type="button"
              onClick={() => { setActiveTab('signup'); setErrorMessage(''); setSuccessMessage(''); }}
              style={{
                flex: 1,
                padding: '10px',
                border: 'none',
                background: 'none',
                fontWeight: activeTab === 'signup' ? '700' : '500',
                color: activeTab === 'signup' ? '#2b6cb0' : '#718096',
                borderBottom: activeTab === 'signup' ? '2px solid #2b6cb0' : 'none',
                cursor: 'pointer',
              }}
            >
              New Registration
            </button>
          </div>

          {errorMessage && (
            <div className="banner banner-error" role="alert">
              {errorMessage}
            </div>
          )}

          {successMessage && (
            <div className="banner banner-success" role="status">
              {successMessage}
            </div>
          )}

          {activeTab === 'login' ? (
            <form onSubmit={handleLoginSubmit} noValidate>
              <div className="form-group">
                <label htmlFor="login-identifier">Email or Username</label>
                <input
                  id="login-identifier"
                  type="text"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. jsmith@example.com"
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="login-password">Password</label>
                <input
                  id="login-password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter password"
                  required
                  disabled={loading}
                />
              </div>

              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Authenticating...' : 'Log In'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleSignupSubmit} noValidate>
              <div className="form-group">
                <label htmlFor="signup-username">Username</label>
                <input
                  id="signup-username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. jsmith_color"
                  required
                  disabled={loading}
                />
                <div className="hint-text">3 to 50 characters, letters, numbers, underscores.</div>
              </div>

              <div className="form-group">
                <label htmlFor="signup-email">Email Address</label>
                <input
                  id="signup-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. jsmith@example.com"
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="signup-password">Password</label>
                <input
                  id="signup-password"
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
          )}
        </>
      )}
    </div>
  );
}
