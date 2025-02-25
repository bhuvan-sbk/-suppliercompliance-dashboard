import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // FastAPI backend URL
  'Content-Type': 'application/json',
});
// Supplier endpoints
export const fetchSuppliers = async () => {
    try {
      const response = await axios.get('http://localhost:8000/suppliers');
      return response.data;
    } catch (error) {
      console.error('Axios Error:', error);
      if (error.response) {
        console.error('Response Data:', error.response.data);
        console.error('Response Status:', error.response.status);
        console.error('Response Headers:', error.response.headers);
      } else if (error.request) {
        console.error('No response received:', error.request);
      } else {
        console.error('Error:', error.message);
      }
      throw error;
    }
  };

export const fetchSupplierDetails = async (supplierId) => {
  return await api.get(`/suppliers/${supplierId}`);
};

// Compliance endpoints
export const uploadComplianceData = async (data) => {
  return await api.post('/suppliers/check-compliance', data);
};

// Insights endpoint
export const fetchInsights = async (supplierId) => {
  return await api.get(`/suppliers/insights/${supplierId}`);
};