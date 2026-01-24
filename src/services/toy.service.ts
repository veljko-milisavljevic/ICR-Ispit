import axios from "axios";
import { ToyModel } from "../models/toy.model";

const client = axios.create({
    baseURL: 'https://toy.pequla.com/api',
    headers: {
        'Accept': 'application/json',
        'X-Name': 'ICR/2025'
    }
})

export class ToyService {
    static async getToys(search: string = '') {
        const rsp = (await client.get<ToyModel[]>(`/toy`))
        const toys = rsp.data
        
        if (!search) return toys

        return toys.filter(
             (toy) => 
                toy.name.toLowerCase().includes(search.toLowerCase()) ||
                toy.description.toLowerCase().includes(search.toLowerCase()) ||
                toy.type.name.toLowerCase().includes(search.toLowerCase())
            )

    }

    static async getToyByPermalink(permalink: string) {
        return (await client.get<ToyModel>(`/toy/permalink/${permalink}`)).data
    }
}