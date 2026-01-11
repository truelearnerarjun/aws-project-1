import React from 'react';

function AddEmpOutput({ data, onNavigate }) {
  const employeeName = data ? `${data.first_name} ${data.last_name}` : 'Employee';

  return (
    <div className="container">
      <div className="header">
        <h1>SAVE SUCCESSFUL</h1>
      </div>

      <div className="success-message">
        <h2>Following Employee has been added to the database</h2>
        <h2>{employeeName}</h2>
      </div>

      <div className="button-group">
        <button onClick={onNavigate}>GO BACK</button>
      </div>
    </div>
  );
}

export default AddEmpOutput;
