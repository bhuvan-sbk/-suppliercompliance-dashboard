import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SupplierList from './components/SupplierList';
import SupplierDetail from './components/SupplierDetail';
// import ComplianceUpload from './components/ComplianceUpload';
import InsightsDashboard from './components/InsightsDashboard';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SupplierList />} />
        <Route path="/suppliers/:supplierId" element={<SupplierDetail />} />
        {/* <Route path="/upload-compliance" element={<ComplianceUpload />} /> */}
        <Route path="/insights/:supplierId" element={<InsightsDashboard />} />
      </Routes>
    </Router>
  );
}