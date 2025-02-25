import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchInsights } from '../services/api';
import { Typography, Paper, Container } from '@mui/material';

export default function InsightsDashboard() {
  const { supplierId } = useParams();
  const [insights, setInsights] = useState('');

  useEffect(() => {
    fetchInsights(supplierId)
      .then((response) => setInsights(response.data.insights))
      .catch((error) => console.error("Failed to fetch insights:", error));
  }, [supplierId]);

  return (
    <Container maxWidth="md">
      <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
        <Typography variant="h4">Compliance Insights</Typography>
        <Typography variant="body1" style={{ marginTop: '20px', whiteSpace: 'pre-wrap' }}>
          {insights}
        </Typography>
      </Paper>
    </Container>
  );
}