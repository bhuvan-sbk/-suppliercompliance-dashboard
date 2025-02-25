import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchSupplierDetails, fetchInsights } from '../services/api';
import { Typography, Paper, List, ListItem, ListItemText, Divider } from '@mui/material';

export default function SupplierDetail() {
  const { supplierId } = useParams();
  const [supplier, setSupplier] = useState(null);
  const [insights, setInsights] = useState('');

  useEffect(() => {
    // Fetch supplier details
    fetchSupplierDetails(supplierId).then((response) => setSupplier(response.data));

    // Fetch insights
    fetchInsights(supplierId).then((response) => setInsights(response.data.insights));
  }, [supplierId]);

  if (!supplier) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Paper elevation={3} style={{ padding: '20px', margin: '20px' }}>
      <Typography variant="h4">{supplier.name}</Typography>
      <Typography variant="subtitle1">Country: {supplier.country}</Typography>
      <Typography variant="subtitle1">Compliance Score: {supplier.compliance_score}</Typography>
      <Typography variant="subtitle1">Last Audit: {supplier.last_audit}</Typography>

      <Divider style={{ margin: '20px 0' }} />

      <Typography variant="h5">Compliance History</Typography>
      <List>
        {supplier.compliance_records?.map((record) => (
          <ListItem key={record.id}>
            <ListItemText
              primary={`Metric: ${record.metric}`}
              secondary={`Result: ${record.result}, Date: ${record.date_recorded}, Status: ${record.status}`}
            />
          </ListItem>
        ))}
      </List>

      <Divider style={{ margin: '20px 0' }} />

      <Typography variant="h5">AI-Generated Insights</Typography>
      <Typography>{insights}</Typography>
    </Paper>
  );
}