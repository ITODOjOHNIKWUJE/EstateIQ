import React, {useEffect, useState} from 'react';
import axios from 'axios';
export default function Home(){const [properties,setProperties]=useState([]);useEffect(()=>{axios.get('http://localhost:5000/api/properties').then(r=>setProperties(r.data)).catch(()=>setProperties([]))},[]);return (<div><h2>Properties</h2><ul>{properties.map(p=><li key={p.id}>{p.title} — {p.address} <small>Units: {p.units.length}</small></li>)}</ul></div>)}
