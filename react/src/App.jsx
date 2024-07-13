import React, { useEffect, useState } from 'react'

const App = () => {
  const [students, setStudents] = useState([])


  useEffect(() => {
    async function getAllStudent() {
      try {
        const students = await axios.get("http://127.0.0.1:8000/em/student/")
        console.log(students.data)
        setStudents(students.data)
      }
      catch (error) {
        console.log(error)
      }
    }
    getAllStudent()
  }, [])
  return (
    <div>
      <h1>connect react js to django</h1>
      {
        students.map((e,i) => {
          return (
      <h2 key={i}>{e.stuname}</h2>
    
          )
        }
  )
}
    </div>
  )
}

export default App