export interface MenuRoute {
	path: string;
	title?: string;
	name?: string;
	icon?: | string | { render: () => void };
	redirect?: string;
	children: MenuRoute[];
	meta: any
}

export type UserInfo = {
	userName: string,
	signature: string,
	userId: string,
	sex: string,
	email: string,
	avatar: string
}

export type UserAvatarList = {
	userHistoryFileList: Array<string>,
	systemAvatarList: Array<string>
};

export type ProjectType = {
	_id: string,
	name: string,
	status: string,
	create_time: string,
	crash_num: number,
	seed_num: number,
	container_id: string,
	user_id: string
};

export type ContainerType = {
	_id: string,
	name: string,
	status: string,
	create_time: string,
	ssh_port: number,
	ws_port: number,
	container_id: string,
	user_id: string
};