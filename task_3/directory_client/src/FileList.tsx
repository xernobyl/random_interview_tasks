/*

*/

import React from 'react'
import './FileList.css'
import { DirectoryService } from './services/directory.service'


class FileList extends React.Component<any, any> {
  path: string[] = []

  constructor(props: any) {
    super(props)
    this.state = {
      items: [],
      loading: false,
    }
  }

  async componentDidMount(): Promise<void> {
    this.loadPath()
  }

  async clickItem(data: any): Promise<void> {
    if (data.type === 'directory') {
      if (!this.state.loading) {
        this.path.push(data.name)
        await this.loadPath()
      }
    }
  }

  async backDir(event: any): Promise<void> {
    if (!this.state.loading) {
      this.path.pop()
      await this.loadPath()
    }
  }

  parseFileData(data: any): any {
    const out = []

    for (const file of data.files) {
      let size: string
      if ('file_size' in file) {
        if (file.file_size > 1024 * 1024 * 1024) {
          size = (file.file_size / (1024 * 1024 * 1024)).toFixed(2).toString() + ' GB'
        } else if (file.file_size > 1024 * 1024) {
          size = (file.file_size / (1024 * 1024)).toFixed(2).toString() + ' MB'
        } else if (file.file_size > 1024) {
          size = (file.file_size / 1024).toFixed(2).toString() + ' KB'
        }
        else {
          size = file.file_size.toString() + ' B'
        }
      } else {
        size = ''
      }

      out.push({
        icon: file.file_type === 'directory' ? '📂' : '📄',
        type: file.file_type,
        name: file.file_name,
        size: size,
      })
    }

    return out
  }

  async loadPath(): Promise<void> {
    const path = this.path.join('/')
    this.setState({ loading: true })
    const data = await DirectoryService.getDirectory(path)
    if ('error' in data) {
      this.setState({ loading: false })
    } else {
      this.setState({
        items: this.parseFileData(data),
        current_path: path,
        loading: false
      })
    }
  }

  render() {
    return (
      <div className="FileList">
        { this.state.loading && <div className="loading-spinner"></div> }
        <header>
          <p>Current directory: { this.path.join('/') }</p>
        </header>
        <table>
          <thead>
            <tr>
              <th>&nbsp;</th>
              <th>Name</th>
              <th>Size</th>
            </tr>
          </thead>
          <tbody>
            {this.path.length !== 0 &&
              <tr className="clickable" onClick={this.backDir.bind(this)}>
                <td>↩️</td>
                <td>..</td>
                <td>&nbsp;</td>
              </tr>
            }
            {this.state.items.map((data: any) => (
              <tr className="clickable" key={data.name} onClick={() => this.clickItem(data)}>
                <td>{data.icon}</td>
                <td>{data.name}</td>
                <td>{data.size}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }
}

export default FileList
