import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";

interface DenseTableProps {
  names: string[];
  amounts: number[];
  percentages: number[];
}

const DenseTable: React.FC<DenseTableProps> = ({
  names,
  amounts,
  percentages,
}) => {
  const rows = names.map((name, index) => ({
    name,
    amount: amounts[index],
    percentage: percentages[index],
  }));

  return (
    <Box sx={{ width: "95%", margin: "10px auto" }}>
      <TableContainer
        component={Paper}
        sx={{
          backgroundColor: "#285bad", // Light blue background
          boxShadow: "none", // Flat design to match dialog
          color: "white", // Text color
        }}
      >
        <Table size="small" aria-label="dense table" sx={{ color: "white" }}>
          <TableHead>
            <TableRow>
              <TableCell>
                <strong>Name</strong>
              </TableCell>
              <TableCell align="right">
                <strong>Amount</strong>
              </TableCell>
              <TableCell align="right">
                <strong>Percentage (%)</strong>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row, idx) => (
              <TableRow key={idx} className="text-white">
                <TableCell component="th" scope="row">
                  {row.name}
                </TableCell>
                <TableCell align="right">
                  {row.amount.toLocaleString()}
                </TableCell>
                <TableCell align="right">{row.percentage}%</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default DenseTable;
