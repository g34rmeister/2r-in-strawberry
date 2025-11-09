import { useState} from "react";

function Droppable({ label, options, value, onChange }) {
  return (
    <div className="droppable">
        <select id={label} value={value} onChange={onChange}>
            <option value="" disabled hidden>
                {label}
            </option>
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