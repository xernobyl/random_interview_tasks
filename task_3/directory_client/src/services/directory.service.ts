import config from "../config.json"

const RE_SPLIT_SLASHES = /\\+|\/+/

export class DirectoryService {

	public static async getDirectory(path: string): Promise<any> {
    // basic path sanitation
    path = path.split(RE_SPLIT_SLASHES).join('/')
		const response = await fetch(config.DIRECTORY_SERVICE + path)
		return await response.json()
	}
}
