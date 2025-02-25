import React, { useEffect, useState } from 'react';
import { fetchSuppliers } from '../services/api';
import { Link } from 'react-router-dom';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

export default function SupplierList() {
  const [suppliers, setSuppliers] = useState([]);

  useEffect(() => {
    fetchSuppliers().then((response) => setSuppliers(response.data));
  }, []);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Country</TableCell>
            <TableCell>Compliance Score</TableCell>
            <TableCell>Last Audit</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {suppliers.map((supplier) => (
            <TableRow key={supplier.id}>
              <TableCell>
                <Link to={`/suppliers/${supplier.id}`}>{supplier.name}</Link>
              </TableCell>
              <TableCell>{supplier.country}</TableCell>
              <TableCell>{supplier.compliance_score}</TableCell>
              <TableCell>{supplier.last_audit}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}