import React from 'react';

function GetEmpOutput({ data, onNavigate }) {
  if (!data) {
    return <div className="container"><div className="loading">Loading...</div></div>;
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Employee Information</h1>
      </div>

      <div className="output-section">
        <div className="output-field">
          <div className="output-label">Employee ID:</div>
          <div className="output-value">{data.id}</div>
        </div>

        <div className="output-field">
          <div className="output-label">First Name:</div>
          <div className="output-value">{data.fname}</div>
        </div>

        <div className="output-field">
          <div className="output-label">Last Name:</div>
          <div className="output-value">{data.lname}</div>
        </div>

        <div className="output-field">
          <div className="output-label">Primary Interest:</div>
          <div className="output-value">{data.interest}</div>
        </div>

        <div className="output-field">
          <div className="output-label">Location:</div>
          <div className="output-value">{data.location}</div>
        </div>

        <div className="output-field">
          <div className="output-label">Image URL:</div>
          <div className="output-value">{data.image_url}</div>
          {data.image_url && (
            <div className="image-container">
              <img src={data.image_url} alt={`${data.fname} ${data.lname}`} />
            </div>
          )}
        </div>
      </div>

      <div className="button-group">
        <button onClick={onNavigate}>RESET</button>
      </div>
    </div>
  );
}

export default GetEmpOutput;
