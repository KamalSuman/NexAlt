import { BarChart } from "@mui/x-charts/BarChart";

export type BarDataProps = {
  columnName: string[];
  amount: number[];
  percentage: number[];
};

const MyBarChart = ({ columnName, amount, percentage }: BarDataProps) => {
  return (
    <BarChart
      xAxis={[
        {
          id: "columns",
          data: columnName,
          scaleType: "band",
          label: "Category",
        },
      ]}
      series={[
        {
          data: amount,
          label: "Amount",
          color: "#3A2FC9",
        },
        {
          data: percentage,
          label: "Percentage",
          color: "#FF6B6B",
        },
      ]}
      height={400}
      width={600}
      margin={{ top: 20, bottom: 50, left: 50, right: 20 }}
    />
  );
};

export default MyBarChart;
