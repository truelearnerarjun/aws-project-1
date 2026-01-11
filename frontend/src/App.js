import React, { useState } from 'react';
import AddEmp from './components/AddEmp';
import GetEmp from './components/GetEmp';
import AddEmpOutput from './components/AddEmpOutput';
import GetEmpOutput from './components/GetEmpOutput';

function App() {
  const [currentPage, setCurrentPage] = useState('addEmp');
  const [addEmpData, setAddEmpData] = useState(null);
  const [getEmpData, setGetEmpData] = useState(null);

  const handleAddEmpSubmit = (data) => {
    setAddEmpData(data);
    setCurrentPage('addEmpOutput');
  };

  const handleGetEmpSubmit = (data) => {
    setGetEmpData(data);
    setCurrentPage('getEmpOutput');
  };

  const goToAddEmp = () => {
    setCurrentPage('addEmp');
    setAddEmpData(null);
  };

  const goToGetEmp = () => {
    setCurrentPage('getEmp');
    setGetEmpData(null);
  };

  return (
    <div className="app">
      {currentPage === 'addEmp' && (
        <AddEmp onSubmit={handleAddEmpSubmit} onNavigate={goToGetEmp} />
      )}
      {currentPage === 'addEmpOutput' && (
        <AddEmpOutput data={addEmpData} onNavigate={goToAddEmp} />
      )}
      {currentPage === 'getEmp' && (
        <GetEmp onSubmit={handleGetEmpSubmit} onNavigate={goToAddEmp} />
      )}
      {currentPage === 'getEmpOutput' && (
        <GetEmpOutput data={getEmpData} onNavigate={goToGetEmp} />
      )}
    </div>
  );
}

export default App;
