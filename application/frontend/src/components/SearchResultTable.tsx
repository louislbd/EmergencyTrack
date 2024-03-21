import React from "react";

interface Location {
  location_x_coordinate: number;
  location_y_coordinate: number;
  department: string;
  [key: string]: any; // Additional fields that might be specific to each department
}

interface Props {
  department: string;
  data: Location[];
}

const SearchResultTable: React.FC<Props> = ({ department, data }) => {
  const renderHeader = () => {
    switch (department) {
      case "blocked_roads":
        return (
          <tr>
            <th>Road Name</th>
            <th>Reason</th>
            <th>Intersection 1</th>
            <th>Intersection 2</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Information</th>
          </tr>
        );
      case "security":
        return (
          <tr>
            <th>Location Name</th>
            <th>Cause of Concern</th>
            <th>Reported Time</th>
            <th>Instructions</th>
          </tr>
        );
      case "weather":
        return (
          <tr>
            <th>Location Name</th>
            <th>event type</th>
            <th>county</th>
            <th>event radius</th>
            <th>Level of Evacuation</th>
            <th>Instructions</th>
          </tr>
        );
      case "wildfires":
        return (
          <tr>
            <th>Location Name</th>
            <th>Cause of Concern</th>
            <th>Reported Time</th>
            <th>Instructions</th>
          </tr>
        );
      default:
        return (
          <tr>
            <th>No data available for this department.</th>
          </tr>
        );
    }
  };

  const renderBody = () => {
    return data.map((item, index) => <tr key={index}>{renderRow(item)}</tr>);
    console.log(data);
  };

  const renderRow = (item: Location) => {
    switch (department) {
      case "blocked_roads":
        return (
          <>
            <td>{item.road_name}</td>
            <td>{item.reason}</td>
            <td>{item.intersection1}</td>
            <td>{item.intersection2}</td>
            <td>{item.starting_datetime}</td>
            <td>{item.ending_datetime}</td>
            <td>{item.informations_for_public}</td>
          </>
        );
      case "security":
        return (
          <>
            <td>{item.location_name}</td>
            <td>{item.cause_of_concern}</td>
            <td>{item.reported_datetime}</td>
            <td>{item.instructions_for_public}</td>
          </>
        );
      case "security":
        return (
          <>
            <td>{item.location_name}</td>
            <td>{item.cause_of_concern}</td>
            <td>{item.reported_datetime}</td>
            <td>{item.instructions_for_public}</td>
          </>
        );
      case "security":
        return (
          <>
            <td>{item.location_name}</td>
            <td>{item.cause_of_concern}</td>
            <td>{item.reported_datetime}</td>
            <td>{item.instructions_for_public}</td>
          </>
        );
      // Add cases for other departments...
      default:
        return <td>No data available for this department.</td>;
    }
  };

  return (
    <table>
      <thead>{renderHeader()}</thead>
      <tbody>{renderBody()}</tbody>
    </table>
  );
};

export default SearchResultTable;
