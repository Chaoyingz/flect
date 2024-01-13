import { AnyComponentList, ComponentProps } from "./components/any-component";
import { useEffect, useState } from "react";

export function Tui() {
    return <Fetch />;
}

function Fetch() {
    const [propsList, setPropsList] = useState<ComponentProps[]>([]);

    useEffect(() => {
        async function fetchComponents() {
            const response = await fetch("https://tui-w8c1.onrender.com/api/");
            const data = await response.json();
            console.log(data);
            setPropsList(data);
        }
        fetchComponents();
    }, []);
    return <Render propsList={propsList} />;
}

function Render(params: { propsList: ComponentProps[] }) {
    return <AnyComponentList propsList={params.propsList} />;
}
