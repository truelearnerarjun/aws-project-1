import React, { useState } from 'react';
import axios from 'axios';

function GetEmp({ onSubmit, onNavigate }) {
  const [empId, setEmpId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post('/fetchdata', {
        emp_id: empId
      });
      onSubmit(response.data);
    } catch (err) {
      setError(err.response?.data || 'Error fetching employee data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Employee Information</h1>
        <h2>Enter Employee ID</h2>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="emp_id">Employee ID:</label>
          <input
            type="number"
            id="emp_id"
            value={empId}
            onChange={(e) => setEmpId(e.target.value)}
            required
            autoFocus
          />
        </div>

        <div className="button-group">
          <button type="submit" disabled={loading}>
            {loading ? 'FETCHING...' : 'FETCH INFO'}
          </button>
          <button type="button" onClick={onNavigate} className="secondary">
            GO TO UPDATE DATABASE PAGE
          </button>
        </div>
      </form>
    </div>
  );
}

export default GetEmp;
