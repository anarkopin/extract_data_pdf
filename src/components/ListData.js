

function ListData ({ data }) {
  


  return (
        <>
 <div className="overflow-x-auto mt-20 lg:p-16 lg:m-28">
  <table className="min-w-full divide-y-2 divide-gray-200 text-sm">
    <thead>
      <tr>
        <th
          className="whitespace-nowrap px-4 py-2 text-left font-medium text-gray-900"
        >
          Registro
        </th>
        <th
          className="whitespace-nowrap px-4 py-2 text-left font-medium text-gray-900"
        >
          Identificador
        </th>
        <th
          className="whitespace-nowrap px-4 py-2 text-left font-medium text-gray-900"
        >
          Tax Filing
        </th>
        <th
          className="whitespace-nowrap px-4 py-2 text-left font-medium text-gray-900"
        >
          Wages
        </th>
        <th
          className="whitespace-nowrap px-4 py-2 text-left font-medium text-gray-900"
        >
          Total Deductions
        </th>
      </tr>
    </thead>

    <tbody className="divide-y divide-gray-200">
        {data && data.map((item) => (
          <tr>
          <td className="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            {item.id}
          </td>
          <td className="whitespace-nowrap px-4 py-2 text-gray-700">{item.identificador}</td>
          <td className="whitespace-nowrap px-4 py-2 text-gray-700">{item.tax_filing}</td>
          <td className="whitespace-nowrap px-4 py-2 text-gray-700">{item.wages}</td>
          <td className="whitespace-nowrap px-4 py-2 text-gray-700">{item.total_deductions}</td>
        </tr>
        ))}

    </tbody>
  </table>
</div>
        </>
    )
}

export default ListData;