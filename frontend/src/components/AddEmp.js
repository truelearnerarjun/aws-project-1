import React, { useState } from 'react';
import axios from 'axios';

function AddEmp({ onSubmit, onNavigate }) {
  const [formData, setFormData] = useState({
    emp_id: '',
    first_name: '',
    last_name: '',
    pri_skill: '',
    location: '',
    emp_image_file: null
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    setFormData(prev => ({
      ...prev,
      emp_image_file: e.target.files[0]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!formData.emp_image_file) {
      setError('Please select a file');
      setLoading(false);
      return;
    }

    const data = new FormData();
    data.append('emp_id', formData.emp_id);
    data.append('first_name', formData.first_name);
    data.append('last_name', formData.last_name);
    data.append('pri_skill', formData.pri_skill);
    data.append('location', formData.location);
    data.append('emp_image_file', formData.emp_image_file);

    try {
      const response = await axios.post('/addemp', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      onSubmit(formData);
    } catch (err) {
      setError(err.response?.data || 'Error adding employee');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Employee Database</h1>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="emp_id">Employee ID:</label>
          <input
            type="number"
            id="emp_id"
            name="emp_id"
            value={formData.emp_id}
            onChange={handleInputChange}
            required
            autoFocus
          />
        </div>

        <div className="form-group">
          <label htmlFor="first_name">First Name:</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="last_name">Last Name:</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="pri_skill">Primary Skills:</label>
          <input
            type="text"
            id="pri_skill"
            name="pri_skill"
            value={formData.pri_skill}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="location">Location:</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="emp_image_file">Image:</label>
          <input
            type="file"
            id="emp_image_file"
            name="emp_image_file"
            onChange={handleFileChange}
            required
          />
        </div>

        <div className="button-group">
          <button type="button" onClick={onNavigate}>
            GET EMPLOYEE INFORMATION
          </button>
          <button type="submit" disabled={loading}>
            {loading ? 'UPDATING...' : 'UPDATE DATABASE'}
          </button>
        </div>
      </form>

      <a href="https://www.intellipaat.com" className="nav-link">About Us</a>
    </div>
  );
}

export default AddEmp;
