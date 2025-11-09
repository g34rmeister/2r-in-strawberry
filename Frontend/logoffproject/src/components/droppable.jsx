import { useState} from "react";

function Droppable({ label, options, value, onChange }) {
  return (
    <div>
      {label && <label htmlFor={label}>{label}</label>}
      <select id={label} value={value} onChange={onChange}>

        {options.map((opt, i) => (
          <option key={i} value={opt.value}>
            {opt.label}
          </option>
        ))}
        
      </select>
    </div>
  );
}

export default Droppable;